from os import link
from time import sleep
import requests
from bs4 import BeautifulSoup
import re
import ast
from kafka import KafkaProducer


def fetch_raw(recipe_url):
    html = None
    print('Processing..{}'.format(recipe_url))
    try:
        r = requests.get(recipe_url, headers=headers)
        if r.status_code == 200:
            html = r.text
    except Exception as ex:
        print('Exception while accessing raw html')
        print(str(ex))
    finally:
        return html.strip()


def get_recipes():
    recipies = []
    salad_url = 'https://www.allrecipes.com/recipes/96/salad/'
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    print('Accessing list')

    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            pattern = r"(?<=\"url\":\s)(\"https://www\..+(?=\s))"
            l = soup.find_all("script")
            links = []
            for link in l:
                links.append(str(link))
            if urls := re.findall(pattern, links[0]):
                idx = 0
                for url in urls:
                    sleep(2)
                    recipe = fetch_raw(ast.literal_eval(url))
                    recipies.append(recipe)
                    idx += 1
                    if idx > 2:
                        break
    except Exception as ex:
        print('Exception in get_recipes')
        print(str(ex))
    finally:
        return recipies


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }

    all_recipes = get_recipes()
    print(all_recipes)
    if len(all_recipes) > 0:
        kafka_producer = connect_kafka_producer()
        for recipe in all_recipes:
            publish_message(kafka_producer, 'raw_recipes',
                            'raw', recipe.strip())
            if kafka_producer is not None:
                kafka_producer.close()
