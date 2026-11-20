-- BROKEN ON PURPOSE. Lock constrains `locked` and says nothing about
-- `alarmArmed`, so Alloy 6 leaves `alarmArmed` free to take any value in the
-- next state. See README.md.

one sig System {
  var locked: lone System,     -- System in locked means the door is locked
  var alarmArmed: lone System  -- System in alarmArmed means the alarm is armed
}

fact Init { no System.locked and some System.alarmArmed }

-- Source: door.py, lock(). Missing a line for alarmArmed.
pred Lock {
  no System.locked
  System.locked' = System
}
-- Source: door.py, unlock().
pred Unlock {
  some System.locked
  System.locked' = none
  System.alarmArmed' = System.alarmArmed
}
pred Stutter {
  System.locked' = System.locked
  System.alarmArmed' = System.alarmArmed
}

fact Behavior { always (Lock or Unlock or Stutter) }

-- Witness: the door actually locks at some point in the trace.
pred DoorLocksAtSomePoint { eventually Lock }

-- "Locking the door never changes whether the alarm is armed." The author
-- believed this always holds, because door.py's lock() never touches the
-- alarm. It does not hold in this model, which is the symptom. See README.md.
assert LockPreservesAlarm { always (Lock implies System.alarmArmed' = System.alarmArmed) }

run DoorLocksAtSomePoint for 3 but 5 steps expect 1
check LockPreservesAlarm for 3 but 5 steps expect 0
