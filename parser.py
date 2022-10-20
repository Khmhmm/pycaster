def _parse_yt(http_addr):
    watch_id = http_addr.split('/')[-1]
    id_args = watch_id.split('?v=')[1]
    id = id_args.split('&')[0]
    return f"https://youtube.com/embed/{id}"

def parse(http_addr):
    return _parse_yt(http_addr)

def get_html(iframelink):
    return '''
<!DOCTYPE html>
<html lang="">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>''' + \
    f'\n<iframe id="player" src="{iframelink}" width="1920" height="1080" frameborder="0" AllowFullScreen allow="fullscreen *"></iframe>\n' + '''
  </body>
</html>
'''

if __name__ == '__main__':
    with open('parser_example.html', 'w') as f:
        iframe_link = parse('https://www.youtube.com/watch?v=3s6_ig3TCwc')
        content = get_html(iframe_link)
        f.write(content)

# "https://www.youtube.com/watch?v=3s6_ig3TCwc"
# "https://www.youtube.com/embed/3s6_ig3TCwc"
