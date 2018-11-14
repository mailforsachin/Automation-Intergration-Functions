var snow = require('./snow');

module.exports = function(context, mySbMsg) {
    context.log('JavaScript ServiceBus queue trigger function processed message:', mySbMsg); 
    var onSuccess = (context, address, incident)=>{
        context.log("Success")
        const bottext = incident.number + " has been created for you";
        const botaddress = mySbMsg.address;
        const channelData = mySbMsg.channelData;
        const data = JSON.stringify({ text:bottext, address:botaddress, channelData:channelData});
        context.bindings.botdata = data;
        context.done();

    };
    var onError = (context, address) => {
        context.log("failed- SNOW is down")
        const txt = 'Sorry! I failed to create an incident. The issue has been reported to my developers. Please try again!';
        const botaddress = mySbMsg.address;
        const channelData = mySbMsg.channelData;
        const data = JSON.stringify({ text:txt, address:botaddress, channelData:channelData});
        context.bindings.botdata = data;
        context.done();

    }
    snow.createSnowTicket(mySbMsg, mySbMsg.address, context, onSuccess, onError);
}





