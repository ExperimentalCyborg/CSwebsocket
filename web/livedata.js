class liveData{
    constructor(url, timeout = 5000) {
        this.socket = io(url, { // url defaults to whatever is in window.location
            autoConnect: false,
            timeout: timeout
        });
    }

    connect(){
        this.socket.connect();
    }

    onConnectionError(callback){
        this.socket.on('connect_error', callback);
    }

    onConnected(callback){
        this.socket.on('connect', callback);
        this.socket.on('reconnect', callback);
    }

    onDisconnected(callback){
        this.socket.on('disconnect', callback);
    }

    //Authentication accepted
    onAuthenticated(callback){
        this.socket.on('authenticated', callback);
    }

    //Session expired or authentication invalid
    onInvalidated(callback){
        this.socket.on('invalidated', callback);
    }

    //Authenticate the session with a session token.
    authenticate(token){
        this.socket.emit('authenticate', token);
    }

    //Receive changes to 'subject' through 'callback'
    subscribe(subject, callback){
        this.socket.on(subject, callback);
        this.socket.emit('subscribe', subject);
    }
}
