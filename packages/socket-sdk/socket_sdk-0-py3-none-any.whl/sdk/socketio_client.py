import socketio 
from .logger import logger

class Client:
    def __init__(self, user_id: str, host: str):
        self.user_id = user_id
        self.host = host
        self.sio = socketio.Client(logger=False, engineio_logger=False)  # Disable built-in logging
        self.register_default_handlers()
        
        logger.info(f"[SIO] Create client         user_id={self.user_id}", extra={"type": "sio"})

    def register_default_handlers(self):
        @self.sio.event
        def connect():
            logger.info(f"[SIO] Connect               user_id={self.user_id}", extra={"type": "sio"})
            print("Connection established")

        @self.sio.event
        def disconnect():
            logger.info(f"[SIO] Disconnect            user_id={self.user_id}", extra={"type": "sio"})
            print("Disconnected from server")

    def event(self, event_name=None):
        def decorator(func):
            if event_name is None:
                event_name_inner = func.__name__
            else:
                event_name_inner = event_name

            @self.sio.on(event_name_inner)
            def wrapper(data):
                logger.info(f"[SIO] Got {event_name_inner} {data}   user_id={self.user_id}", extra={"type": "sio"})
                try:
                    func(data)
                except Exception as e:
                    logger.error(f"[SIO] Error in event handler '{event_name_inner}': {e}", extra={"type": "sio"})
                    print(f"Error in event handler '{event_name_inner}': {e}")

            return func

        return decorator

    def connect(self):
        try:
            self.sio.connect(self.host, transports=['websocket'])
        except socketio.exceptions.ConnectionError as e:
            logger.error(f"[SIO] Connect               user_id={self.user_id} -> Connection Error: {e}", extra={"type": "sio"})
            raise
        except Exception as e:
            logger.error(f"[SIO] Connect               user_id={self.user_id} -> Unexpected Error: {e}", extra={"type": "sio"})
            raise

    def joinLobby(self, lobby_id: str):
        payload = {"lobbyId": lobby_id, "userId": self.user_id}
        try:
            self.sio.emit("joinLobby", payload)
            logger.info(f"[SIO] Emit joinLobby {payload} user_id={self.user_id}", extra={"type": "sio"})
            print("Lobby joined")
        except socketio.exceptions.ConnectionError as e:
            logger.error(f"[SIO] Emit joinLobby {payload} user_id={self.user_id} -> Connection Error: {e}", extra={"type": "sio"})
            raise
        except Exception as e:
            logger.error(f"[SIO] Emit joinLobby {payload} user_id={self.user_id} -> Unexpected Error: {e}", extra={"type": "sio"})
            raise

    def startSwipes(self):
        try:
            self.sio.emit("startSwipes")
            logger.info(f"[SIO] Emit startSwipes      user_id={self.user_id}", extra={"type": "sio"})
            print("Swipes started")
        except socketio.exceptions.ConnectionError as e:
            logger.error(f"[SIO] Emit startSwipes      user_id={self.user_id} -> Connection Error: {e}", extra={"type": "sio"})
            raise
        except Exception as e:
            logger.error(f"[SIO] Emit startSwipes      user_id={self.user_id} -> Unexpected Error: {e}", extra={"type": "sio"})
            raise

    def disconnect(self):
        try:
            self.sio.disconnect()
        except socketio.exceptions.ConnectionError as e:
            logger.error(f"[SIO] Disconnect            user_id={self.user_id} -> Connection Error: {e}", extra={"type": "sio"})
            raise
        except Exception as e:
            logger.error(f"[SIO] Disconnect            user_id={self.user_id} -> Unexpected Error: {e}", extra={"type": "sio"})
            raise
