# Source here: https://www.python-engineer.com/posts/notion-api-python/

from datetime import datetime, timezone

from requests import delete

from utils import delete_page, get_pages, create_page, update_page, get_page_id, delete_page

def run_get_pages():
    pages = get_pages()

    for page in pages:
        page_id = page["id"]
        props = page["properties"]
        url = props["URL"]["title"][0]["text"]["content"]
        title = props["Title"]["rich_text"][0]["text"]["content"]
        published = props["Published"]["date"]["start"]
        published = datetime.fromisoformat(published)
        print(url, title, published)

def run_create_page():
    title = "Test Title"
    description = "Test Description"
    published_date = datetime.now().astimezone(timezone.utc).isoformat()
    data = {
        "URL": {"title": [{"text": {"content": description}}]},
        "Title": {"rich_text": [{"text": {"content": title}}]},
        "Published": {"date": {"start": published_date, "end": None}}
    }

    create_page(data)

def run_update_page():
    page_id = get_page_id(index=-2)

    new_date = datetime(2023, 1, 15).astimezone(timezone.utc).isoformat()
    update_data = {"Published": {"date": {"start": new_date, "end": None}}}

    update_page(page_id, update_data)

def run_delete_page():
    page_id = get_page_id(index=-1)

    delete_page(page_id)


if __name__ == "__main__":
    run_get_pages()
    run_create_page()
    run_update_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    run_delete_page()
    