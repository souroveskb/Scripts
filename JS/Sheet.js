
function hsFollowUp() {

  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var calendarID = spreadsheet.getRange("z2").getValue();
  var eventCal = CalendarApp.getCalendarById(calendarID);

  var eventIds = spreadsheet.getRange("z3:z75").getValues();  //event IDs are hidden in the sheet

  var professorInfo = spreadsheet.getRange("B3:C75").getValues(); // 2D array for the information of the professors
  var followUpTime = spreadsheet.getRange("L3:L75").getValues();  // follow up time given by them


  for(x=0, idx = 3; x < followUpTime.length; x++, idx++){

    if(followUpTime[x] != ""){
      var nameTitle = professorInfo[x][1] + " from " + professorInfo[x][0];
      var followUp = followUpTime[x][0];

      // followUp.setMinutes(0);
      // Logger.log(nameTitle + " " + (followUp));

      //fetches if there's already an event
      var oldEvent = eventIds[x][0];
      var eventId = 'Z' + idx;
      var existEvent = eventCal.getEventById(oldEvent);


      if(!existEvent){// If there's not any existing event then we proceed
        var event = eventCal.createAllDayEvent(nameTitle, followUp);
        var cell = spreadsheet.getRange(eventId);
        cell.setValue(event.getId());
        // Events set
        Logger.log("Event set")

      } else {// If event already exists but something changed
        var existEventTitle = existEvent.getTitle();
        var existEventTime = existEvent.getAllDayStartDate();
        if (existEventTitle != nameTitle) {
          existEvent.setTitle(nameTitle);
        } 

        if (existEventTime.getDate() != followUp.getDate()) {
          existEvent.setAllDayDate(followUp);
          Logger.log("times rescheduled");
        }  
      }
    }
  }
  SpreadsheetApp.getUi() // Or DocumentApp or FormApp.
     .alert('The events are updated!!');
}

//making a menu component
function onOpen(){
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Set Event')
  .addItem('Sync Followup', 'hsFollowUp')
  .addToUi();
}



