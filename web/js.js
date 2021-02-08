function updateSomeStatistic(newValue){
    document.getElementById('someStatistic').innerHTML = newValue;
}

const dataSource = new liveData();

dataSource.onAuthenticated(() => {
    console.log('Authenticated.');
    dataSource.subscribe('counter1', updateSomeStatistic);
    console.log('Subscribed to counter1.');
});

dataSource.onInvalidated(() => {
    alert('Session expired. Please log in again.'); // alerts suck but you get the idea
});

dataSource.onConnected(()=>{
    dataSource.authenticate(Math.random());
});

dataSource.onDisconnected(reason =>{
    console.error('Disconnected: ' + reason);
});

dataSource.onConnectionError(error =>{
    console.error('Failed to connect websocket: ' + error);
});

dataSource.connect();
