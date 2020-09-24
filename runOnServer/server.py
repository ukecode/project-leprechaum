import pika, sys, os
from pytorrent import torrentClass 
from decouple import config

def main():
    
    TORRENT_LOGIN = config('TORRENT_LOGIN')
    TORRENT_PASSWORD = config('TORRENT_PASSWORD')
    
    torrent_login = TORRENT_LOGIN
    torrent_password = TORRENT_PASSWORD
    auth = f"{torrent_login}:{torrent_password}"
    torrent = torrentClass(auth)
    
    CLOUDAMQP_URL = config('CLOUDAMQP_URL')
    url = os.environ.get('CLOUDAMQP_URL', CLOUDAMQP_URL)
    params = pika.URLParameters(url)

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    USERNAME = config('USERNAME')
    channel.queue_declare(queue=USERNAME)

    def callback(ch, method, properties, body):
        ret = torrent.download_new_torrent(body)

    channel.basic_consume(queue=USERNAME, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)