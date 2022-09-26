/* addEventListener(name, function, capture_mode)

capture_mode is a boolean that determines when the 
element will receive the event listener.

True:  Events will be run in capturing phase. This
       means that events will first fire on the 
       outer document element, and then fire on the
       next child, etc. All the way until it reaches
       the element that we added the event listener.
False: Events will be run in bubbling phase. This
       means that they will fire first on the 
       element that we attached the event to, and
       work its way out to the root document. This
       is the default value.
*/