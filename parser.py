IFRAME_HEIGHT = "900"

def _parse_yt(http_addr):
    watch_id = http_addr.split('/')[-1]
    id_args = watch_id.split('?v=')[1]
    id = id_args.split('&')[0]
    return f"https://youtube.com/embed/{id}"


def _parse_ytbe(http_addr):
    watch_id = http_addr.split('/')[-1]
    return f"https://youtube.com/embed/{watch_id}"


def _get_html_by_link(iframelink):
    return '''
<!DOCTYPE html>
<html lang="">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>''' + \
    f'\n<iframe id="player" src="{iframelink}" width="100%" height="{IFRAME_HEIGHT}" frameborder="0" AllowFullScreen allow="fullscreen *"></iframe>\n' + '''
  </body>
</html>
'''


def _get_html_by_iframe(iframe):
    # <iframe ID="player" src=... />
    #         ^^^^^^^^^^^
    d = _to_dict(iframe)
    d['id'] = 'player'
    d['width'] = '100%'
    # NOTE: 100% cause very small height
    d['height'] = IFRAME_HEIGHT
    d['frameborder'] = '0' 
    iframe = _from_dict(d)
    return '''
    <!DOCTYPE html>
<html lang="">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>''' + \
    iframe + '''
  </body>
</html>
    '''


def _to_dict(iframe):
    iframe = iframe.replace('<iframe', '').replace('></iframe>', '')
    params = iframe.split('" ')
    i = 0
    while True:
        if i >= len(params):
          break
        if params[i] == '' or '=' not in params[i]:
          del params[i]
          continue
        i += 1

    return {p.split('="')[0].replace(' ', ''): p.split('="')[1].replace('"', '') for p in params}


def _from_dict(iframe_d):
    params = [f'{k}="{v}"' for k, v in iframe_d.items()]
    return '<iframe ' + ' '.join(params) + '></iframe>'


NO_CONTENT = _get_html_by_link('file://nocontent.html')


def parse(something):
      if '</iframe>' in something:
          return _get_html_by_iframe(something)
      
      http_addr = something
      if 'youtube.com' in http_addr:
          return _get_html_by_link(_parse_yt(http_addr))
      elif 'youtu.be' in http_addr:
          return _get_html_by_link(_parse_ytbe(http_addr))
      else:
          return NO_CONTENT


if __name__ == '__main__':
    with open('parser_example.html', 'w') as f:
        content = parse(''' <iframe src="https://vk.com/video_ext.php?oid=-18213107&id=456239605&hash=8a9e706c52e9247f&hd=1" width="640" height="360" allow="autoplay; encrypted-media; fullscreen; picture-in-picture;" frameborder="0" allowfullscreen></iframe> ''')
        f.write(content)

# "https://www.youtube.com/watch?v=3s6_ig3TCwc"
# "https://www.youtube.com/embed/3s6_ig3TCwc"
