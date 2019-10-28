#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template, request, Response, send_from_directory
from utils.rabbitmq_exchange import Reader, Sender
from utils.cpu_util import CpuUtil
from stream import Stream

from options import parse_options

app = Flask(__name__)
parser, settings = None, None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_stream')
def video_stream():
    def new_frame(stream):
        while True:
            frame = stream.get_frame()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(new_frame(Stream()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_rabbit_msg')
def get_rabbit_msg():
    global settings
    uuid = request.args.get('uuid')
    recv = Reader(uuid=uuid,
                  host=settings.rabbit_host,
                  port=int(settings.rabbit_port),
                  credentials=[settings.rabbit_login, settings.rabbit_psw])
    return json.dumps({'msg': recv.receive_msg()}, ensure_ascii=False)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


def main(argv=None):
    global parser, settings
    parser, settings = parse_options(argv)

    cpu_util = CpuUtil(load_limit=int(settings.cpu_load_limit))
    cpu_util.load_limit = int(settings.cpu_load_limit)
    cpu_util.daemon = True
    cpu_util.start()

    Sender.host = settings.rabbit_host
    Sender.port = int(settings.rabbit_port)
    Sender.credentials = [settings.rabbit_login, settings.rabbit_psw]

    app.run(host='0.0.0.0', threaded=True)


if __name__ == '__main__':
    main()
