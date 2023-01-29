import covalent as ct
from bs4 import BeautifulSoup 
import requests, random
import json
import pickle
import urllib.parse

# Define constants

NUM_PAGES_TO_SEARCH = 16

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

def add_post(struct, title, url, comments_url, post_data=None):
      posts = struct['posts']
      posts.append({
            'title': title,
            'url': url,
            'commentsUrl': comments_url,
            'postData': post_data
      })


# Helper functions

def set_author(struct, author):
    struct['author'] = author

def set_time(struct, time):
    struct['time'] = time

def set_score(struct, score):
    struct['score'] = score

def set_link_flair(struct, link_flair):
    struct['linkFlair'] = link_flair

def set_post_content(struct, postContent):
    struct['postContent'] = postContent

def add_comment(struct, comment, score, permalink):
    comments = struct['comments']
    comments.append({
            'comment': comment,
            'score': score,
            'permalink': permalink
    })

@ct.electron
def scrape_post(url):

    # Set up data structures
    post_data = {
        'author': None,
        'time': None,
        'score': None,
        'linkFlair': None,
        'postContent': None, # later extend to include image data and captions
        'comments': []
    }

    for _ in user_agent_list:

        #Pick a random user agent
        user_agent = random.choice(user_agent_list)
        #Set the headers 
        headers = {'User-Agent': user_agent}
    try:
        soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
        post_section = soup.find('div', {'class': 'sitetable linklisting'})
    except Exception as e:
        pass
    try:
        author = post_section.find('a', {'class': 'author'}).text
        set_author(post_data, author)
    except:
        pass
    try:
        time = post_section.find('time').get('datetime')
        set_time(post_data, time)
    except:
        pass

    try:
        score = post_section.find('div', {'class': 'score unvoted'}).get('title')
        set_score(post_data, score)
    except:
        pass

    try:
        link_flair = post_section.find('span', {'class': 'linkflairlabel'}).get('title')
        set_link_flair(post_data, link_flair)
    except:
        pass
    try:
        post_content = post_section.find('div', {'class': ['usertext-body', 'may-blank-within']})
        if post_content:
            post_content_elements = post_content.find_all('p')
            combined_content = "".join([p.text for p in post_content_elements]) if post_content_elements else None
            set_post_content(post_data, combined_content)
    except:
        pass

    # Retrieve comments data
    try:
        comment_section = soup.find('div', 'commentarea').find('div', {'class': ['sitetable', 'nestedlisting']})
        top_level_comments = comment_section.find_all('div', {'class': ['comment', 'noncollapsed']}, recursive=False) if comment_section else []
        for comment in top_level_comments:
            comment_body = comment.find('div', {'class': ['usertext-body', 'may-blank-within']})
            comment_body_paragraphs = comment_body.find_all('p') if comment_body else []
            combined_comment_body = " ".join([p.text for p in comment_body_paragraphs])
            score = comment.find('span', {'class': ['score', 'unvoted']})
            score = score.get('title') if score else None
            links = comment.find('ul', {'class': ['flat-list', 'buttons']}).find('li', {'class': 'first'})
            permalink = links.find('a').get('href') if links else None
            add_comment(post_data, combined_comment_body, score, permalink)
    except Exception as e:
        pass   
    return post_data

@ct.lattice
def scrape_page(query):
    search_results = {
      'name': query,
      'posts': [],
    }
    for _ in user_agent_list:
        
        #Pick a random user agent
        user_agent = random.choice(user_agent_list)
        #Set the headers 
        headers = {'User-Agent': user_agent}

    url = f"https://old.reddit.com/search?q={urllib.parse.quote(query)}&sort=relevance"
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

    total_posts = 0
    for i in range(NUM_PAGES_TO_SEARCH):
        for _ in user_agent_list:
            #Pick a random user agent
            user_agent = random.choice(user_agent_list)

            #Set the headers 
            headers = {'User-Agent': user_agent}

        soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

        posts = soup.find_all('div', {'class': 'search-result-link'})
        for post in posts:
                total_posts += 1
                if post.find('span', {'class': 'promoted-tag'}):
                    continue
                post_title = post.find('a', {'class': ['search-title']})
                comments_url = post.find('a', {'class': 'search-comments'})
                if not comments_url:
                    continue
                comments_url = comments_url['href']
                post_content = scrape_post(comments_url)
                add_post(search_results, post_title.text, post_title['href'], comments_url, post_content)
        try:
            url_groups = soup.find_all('span', {'class': 'nextprev'})
            url = url_groups[1].find('a', {'rel': 'next'}).get('href') if len(url_groups) >= 2 else url_groups[0].find('a', {'rel': 'next'}).get('href')
        except:
            continue
    return search_results
    
def get_data(query):
    # Dispatch the workflow
    dispatch_id = ct.dispatch(scrape_page)(query)
    result = ct.get_result(dispatch_id)
    print(result)
    return result


