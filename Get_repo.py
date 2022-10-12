
import time
import random
import urllib.request
import json


def get_tokens():
    tokens = ["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",
              "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",
              "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",
              "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",
              "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",
              "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"]  # this list contain tokens, each token should be in quotation
    return tokens


class GitHub:
    def __init__(self, url, ct):
        self.ct = ct
        self.url = url

    def getResponse(self):
        jsonData = None
        try:
            if self.ct == len(get_tokens()):
                self.ct = 0
            reqr = urllib.request.Request(self.url)
            reqr.add_header('Authorization', 'token %s' % get_tokens()[self.ct])
            opener = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
            content = opener.open(reqr).read()
            self.ct += 1
            jsonData = json.loads(content)
        except Exception as e:
            pass
            print(e, self.url, self.ct)
        return jsonData, self.ct


class GitHubMeta:
    def __init__(self, config, ct):
        self.ct = ct
        self.config = config

    def get_repos(self):
        data = []

        p = 1

        while True:
            url2 = 'https://api.github.com/search/code?q=' + self.config + '+in:file+size:>=0+language:python' \
                                                                           '+page=' + str(p) + '&per_page=100 '
            data_arrays, self.ct = GitHub(url2, self.ct).getResponse()
            p += 1
            if data_arrays is not None:
                if p == 50:
                    break
                data += data_arrays['items']
            else:
                break
            time.sleep(random.choice(list(range(70, 80))))
        print(self.ct)
        return data, self.ct


path_output = './data/'


def save_json(content, output_file, mode='w'):
    with open(output_file, mode) as filey:
        filey.writelines(json.dumps(content, indent=4))
    return output_file


def main():
    config = ["import%2Btorch",
              "import%2Btensorflow",
              "import%2Bkeras",
              "from%2BTheano%2Bimport%2Btensor",
              "from%2Bsklearn",
              "import%2Bcaffe",
              "import%2Bmxnet"]
    for conf in config:
        ct = 0
        data, ct = GitHubMeta(conf, ct).get_repos()
        print(conf, ' total repos:', len(data))
        save_json(data, path_output+'{}.json'.format(conf))
        time.sleep(random.choice(list(range(70, 80))))


if __name__ == '__main__':
    main()
