module.exports = function (context, myQueueItem) {
    context.log('Sending Bot message', myQueueItem);

    var message = {
        'text': myQueueItem.text,
        'address': myQueueItem.address,
        'channelData': myQueueItem.channelData
    };

    context.log(message)
    context.done(null, message)
    
}