import json
import shutil
import time
from copy import copy
from datetime import datetime, timedelta
from logging import getLogger
from os.path import exists, join, expanduser
from threading import Thread, Event

from xdg import BaseDirectory as XDG

from chatterbox_bus_client.message import Message
from chatterbox_bus_client.util import dtparser, to_local
from combo_lock import NamedLock

LOG = getLogger("BUS")

SCHEDULE_FILE = join(XDG.xdg_data_home, "chatterbox",
                     "chatterbox_schedule.json")


class ChatterboxScheduledEvent:
    def __init__(self, when, event_name, skill_id, handler_name, repeat=0,
                 data=None, context=None):
        self.skill_id = skill_id
        self.event_name = event_name
        self.handler_name = handler_name
        self.when = self.normalize_when(when)
        self.repeat = repeat
        self.data = data or {}
        self.context = context or {}
        self.next_ts = self.get_repeat_time()

    @property
    def bus_message(self):
        return ".".join([self.skill_id, self.event_name, self.handler_name,
                         str(self.when)])

    @staticmethod
    def from_json(data):
        if isinstance(data, str):
            data = json.loads(data)
        return ChatterboxScheduledEvent(**data)

    @property
    def as_json(self):
        return {
            "skill_id": self.skill_id,
            "event_name": self.event_name,
            "handler_name": self.handler_name,
            "when": self.when,
            "repeat": self.repeat,
            "data": self.data,
            "context": self.context
        }

    @property
    def time_left(self):
        return self.when - time.time()

    @property
    def is_repeating(self):
        return self.repeat > 0

    @property
    def is_expired(self):
        """ scheduled date is in the past """
        return self.when < time.time()

    @property
    def repeat_time(self):
        """Next scheduled time for repeating event. Guarantees that the
        time is not in the past (but could skip interim events)

        Returns: (float) time for next event
        """
        return self.next_ts

    def get_repeat_time(self):
        """Next scheduled time for repeating event. Guarantees that the
        time is not in the past (but could skip interim events)

        Returns: (float) time for next event
        """
        next_time = self.when + self.repeat
        while next_time < time.time():
            # Schedule at an offset to assure no doubles
            next_time = time.time() + abs(self.repeat)
        return next_time

    @property
    def datetime(self):
        """ datetime when event is scheduled, in local timezone """
        dt = datetime.fromtimestamp(self.when)
        return to_local(dt)

    @property
    def repeat_datetime(self):
        """ datetime when event will fire next, in local timezone """
        dt = datetime.fromtimestamp(self.repeat_time)
        return to_local(dt)

    @staticmethod
    def normalize_when(when):
        unix_ts = -1
        if isinstance(when, str):
            try:
                when = float(when)  # unix_ts
            except:
                if dtparser:
                    when = dtparser.parse(when)  # hopefully some ISO date
                else:
                    raise
        if isinstance(when, (float, int)):
            unix_ts = when
        if isinstance(when, timedelta):
            when = datetime.now() + timedelta
        if isinstance(when, datetime):
            unix_ts = when.timestamp()
        return unix_ts


class EventScheduler(Thread):
    def __init__(self, bus):
        """
            Create an event scheduler thread. Will send messages at a
            predetermined time to the registered targets.

            Args:
                bus:
                   chatterbox messagebus (chatterbox.messagebus)
        """
        super().__init__()
        self._last_saved = {}
        self.schedule = {}

        self.bus = bus
        self.stop_event = Event()

        self.bus.on('chatterbox.scheduler.schedule_event',
                    self.schedule_event_handler)
        self.bus.on('chatterbox.scheduler.remove_event',
                    self.remove_event_handler)
        self.bus.on('chatterbox.scheduler.update_event',
                    self.update_event_handler)
        self.bus.on('chatterbox.scheduler.get_event',
                    self.get_event_handler)
        self.bus.on('chatterbox.scheduler.clear_expired',
                    self.handle_clear_expired)
        self.bus.on('chatterbox.scheduler.get_expired',
                    self.handle_get_expired)

        # do not fire ancient timers
        # TODO reconsider if we want this, if you set an alarm, shutdown
        #  chatterbox, and turn it back on after the alarm time
        #  (next day... or next year), what should happen?
        self.bus.emit(Message('chatterbox.scheduler.clear_expired'))

    @property
    def events(self):
        events = []
        for event_list in self.schedule.values():
            events += event_list
        return sorted(events, key=lambda k: k.when)

    @property
    def expired_events(self):
        expired = []
        for event_name, event_list in self.schedule.items():
            expired += [e for e in event_list if e.is_expired]
        return expired

    @property
    def json_schedule(self):
        schedule_json = {}
        for name, event_list in self.schedule.items():
            schedule_json[name] = [e.as_json for e in event_list]
        return schedule_json

    # scheduler interface
    def add_to_schedule(self, event):
        LOG.info(f"adding to schedule: {event.event_name}")
        if event.event_name not in self.schedule:
            self.schedule[event.event_name] = []
        self.schedule[event.event_name].append(event)

    def remove_from_schedule(self, event):
        if event.event_name in self.schedule:
            LOG.info(f"removing from schedule: {event.event_name}")
            events = self.schedule[event.event_name]
            for idx, e in enumerate(events):
                if event.as_json == e.as_json:
                    events[idx] = None
            self.schedule[event.event_name] = [e for e in events if e]
            if not self.schedule[event.event_name]:
                self.schedule.pop(event.event_name)

    def update_event_data(self, event):
        # ASSUMPTION: only data should be replaced
        # all fields except data/context must match an existing event
        base_event = {k: v for k, v in event.as_json.items()
                      if k not in ["data", "context"]}
        events = self.schedule[event.event_name]
        for idx, e in enumerate(events):
            base_event2 = {k: v for k, v in e.as_json.items()
                           if k not in ["data", "context"]}
            if base_event2 == base_event:
                # reset event if it is an active repeating event
                if event.repeat:
                    event.when = time.time()
                events[idx] = event
        self.schedule[event.event_name] = event

    def update_event(self, name, idx, event):
        self.schedule[name][idx] = event

    def clear_expired(self):
        """
            Remove repeating events from events dict.
        """
        for e in self.expired_events:
            self.remove_from_schedule(e)

    def clear_empty(self):
        """
            Remove empty event entries from events dict
        """
        self.schedule = {k: v for k, v in self.schedule.items() if v}

    # file interface
    @staticmethod
    def load_schedule(fallback=True):
        with NamedLock('chatterbox-scheduler'):
            if not exists(SCHEDULE_FILE):
                return {}
            try:
                with open(expanduser(SCHEDULE_FILE), "r") as f:
                    return json.load(f)
            except Exception as e:
                LOG.error("OH SNAP, schedule file is corrupted!!")
        if fallback:
            EventScheduler.restore_backup()
            return EventScheduler.load_schedule(fallback=False)
        return {}

    def load(self):
        """read current schedule from disk."""
        schedule_json = self.load_schedule()
        for name, event_list in schedule_json.items():
            self.schedule[name] = [ChatterboxScheduledEvent.from_json(e) for e
                                   in event_list]

    def backup(self, backup_file=None):
        # backup schedule file
        backup_file = backup_file or SCHEDULE_FILE + ".bak"
        with NamedLock('chatterbox-scheduler'):
            if exists(SCHEDULE_FILE):
                try:
                    # confirm that schedule is valid json
                    with open(expanduser(SCHEDULE_FILE), "r") as f:
                        data = json.load(f)
                    shutil.copyfile(SCHEDULE_FILE, backup_file)
                    LOG.debug(f"backed up schedule file to {backup_file}")
                except:
                    corrupted_bak = backup_file + ".corrupted"
                    shutil.copyfile(SCHEDULE_FILE, backup_file + ".corrupted")
                    LOG.error(
                        f"existing schedule file is corrupted, backed up to {corrupted_bak}")
            else:
                try:
                    # save new file
                    with open(backup_file, 'w') as f:
                        json.dump(self.json_schedule, f, indent=2)
                    LOG.debug(f"saved schedule file to {backup_file}")
                except:
                    LOG.debug("schedule file backup failed")

    @staticmethod
    def restore_backup(backup_file=None):
        backup_file = backup_file or SCHEDULE_FILE + ".bak"
        with NamedLock('chatterbox-scheduler'):
            if exists(backup_file):
                try:
                    # If backup is valid json restore it
                    with open(expanduser(backup_file), "r") as f:
                        data = json.load(f)
                    shutil.copyfile(backup_file, SCHEDULE_FILE)
                    LOG.info("restored schedule backup")
                except:
                    LOG.info("schedule backup is corrupted!!")
            else:
                LOG.info("no schedule backup found to restore")

    def store(self):
        """
            Write current schedule to disk.
        """
        # if data didn't change, don't save
        if self._last_saved == self.json_schedule:
            return

        # backup old file
        self.backup()

        # save new file
        with NamedLock('chatterbox-scheduler'):
            with open(SCHEDULE_FILE, 'w') as f:
                json.dump(self.json_schedule, f, indent=2)

            # verify saving worked
            try:
                with open(expanduser(SCHEDULE_FILE), "r") as f:
                    data = json.load(f)
            except Exception as e:
                # try again
                try:
                    with open(SCHEDULE_FILE, 'w') as f:
                        json.dump(self.json_schedule, f, indent=2)
                    with open(expanduser(SCHEDULE_FILE), "r") as f:
                        data = json.load(f)
                except Exception as e:
                    # restore backup
                    LOG.error("Failed to save schedule,"
                              "schedule file is corrupted!!")

        # track so we dont store all the time
        self._last_saved = copy(self.json_schedule)

    # events interface
    @staticmethod
    def message2event(message):
        event = message.data["event_name"]
        sched_time = message.data["when"]
        repeat = message.data.get('repeat', 0)
        data = message.data.get('data', {})
        skill_id = message.data.get("skill_id") or \
                   message.context.get("skill_id") or \
                   message.context.get("source") or "anon"
        handler = message.data.get("handler_name") or f"handle_{event}"
        return ChatterboxScheduledEvent(sched_time, event, skill_id, handler,
                                        repeat, data)

    def schedule_event_handler(self, message):
        """
        Messagebus interface to the schedule_event method.
        Required data in the message envelope is
            event: event to emit
            time:  time to emit the event

        optional data is
            repeat: repeat interval
            data:   data to send along with the event
        """
        event = self.message2event(message)
        self.add_to_schedule(event)

    def remove_event_handler(self, message):
        """ Messagebus interface to the remove_event method. """
        event = self.message2event(message)
        self.remove_from_schedule(event)

    def update_event_handler(self, message):
        """ Messagebus interface to the update_event method. """
        event = self.message2event(message)
        self.update_event_data(event)

    def get_event_handler(self, message):
        """
            Messagebus interface to get_event.
            Emits another event sending event status
        """
        event = self.message2event(message)
        if event.event_name in self.schedule:
            msg_type = f'chatterbox.event_status.callback.{event.event_name}'
            msg_data = event.as_json
        else:
            msg_type = f'chatterbox.event_error.callback.{event.event_name}'
            msg_data = {"error": "event is not scheduled"}
        self.bus.emit(message.reply(msg_type, msg_data))

    def handle_get_expired(self, message):
        events = [e.as_json for e in self.expired_events]
        # TODO skill_id from message and filter
        self.bus.emit(Message('chatterbox.scheduler.expired_list',
                              {"events": events}))

    def handle_clear_expired(self, message):
        self.clear_expired()

    # thread
    def check_state(self):
        """
            Check if an event should be triggered.
        """
        msgs_to_send = []
        old_sched = dict(self.schedule)

        # Check all events
        for event_name, event_list in self.schedule.items():
            for idx, event in enumerate(event_list):
                if event.is_expired and not event.is_repeating:
                    LOG.info(f"scheduled event expired {event.event_name}")
                    msgs_to_send.append(
                        Message(event.bus_message, event.data))

                    # delete expired event
                    self.remove_from_schedule(event)
                    msgs_to_send.append(
                        Message(event.bus_message + ".expired",
                                event.data))

                elif event.is_expired and \
                        event.repeat_time < time.time():
                    LOG.info(f"repeating scheduled event expired"
                             f" {event.event_name}")
                    msgs_to_send.append(
                        Message(event.bus_message, event.data))
                    msgs_to_send.append(
                        Message(event.bus_message + ".expired",
                                event.data))
                    # update next trigger time
                    self.schedule[event_name][idx].next_ts = \
                        event.get_repeat_time()

        self.store()

        if old_sched != self.schedule:
            msgs_to_send.append(Message(
                'chatterbox.scheduler.schedule.sync', self.json_schedule))
        for m in msgs_to_send:
            self.bus.emit(m)

    def run(self):
        self.load()
        self.stop_event.clear()
        while not self.stop_event.is_set():
            self.check_state()

    def shutdown(self):
        """ Stop the running thread. """
        self.stop_event.set()
        # Remove listeners
        self.bus.remove_all_listeners('chatterbox.scheduler.schedule_event')
        self.bus.remove_all_listeners('chatterbox.scheduler.remove_event')
        self.bus.remove_all_listeners('chatterbox.scheduler.update_event')
        self.bus.remove_all_listeners('chatterbox.scheduler.clear_repeating')
        self.bus.remove_all_listeners('chatterbox.scheduler.get_expired')
        # Wait for thread to finish
        self.join()
        # Prune event list in preparation for saving
        self.clear_expired()
        self.clear_empty()
        # Store all pending scheduled events
        self.store()
