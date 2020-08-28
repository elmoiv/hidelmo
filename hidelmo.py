import sys, requests, random

userAgents = '''Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36
Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36
Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'''

def hideMe(url, filename):
    data = {
        "u":url,
        "encodeURL":"1"
    }
    headers = {
        "user-agent":random.choice(userAgents.split('\n'))
    }

    # Content type should anything but html
    d = "text/html; charset=UTF-8"
    n = 0
    
    # Connecting in a loop till our death or server responds lol.
    with open(filename, 'wb') as f:
        while(d == "text/html; charset=UTF-8"):
            n += 1
            print(f"Connecting to Hide.me... {n}")
            
            response = requests.post(
                "https://nl.hideproxy.me/includes/process.php?action=update",
                data=data,
                headers=headers,
                stream=True
                )

            d = response.headers.get('content-type')

        total = response.headers.get('content-length')
        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)

            for data in response.iter_content(chunk_size=max(int(total / 1000), 1 << 20)):
                f.write(data)
                downloaded += len(data)
                percent = int(50 * downloaded / total)
                r_size = total / (1 << 20)
                d_size = downloaded / (1 << 20)
                print(
                    '\r[{}{}] '.format(
                                    '█' * percent,
                                    ' ' * (50 - percent)
                                       ) \
                    + '[{0:.2f}/{1:.2f} MB]'.format(
                                        d_size,
                                        r_size
                                        ),
                    end='\r')

    print()

if __name__ == '__main__':
    url, name = sys.argv[1:3]
    hideMe(eval(f'"{url}"'), name)
