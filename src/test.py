import requests
from bs4 import BeautifulSoup

def print_secret_message(doc_url):
    response = requests.get(doc_url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    if not table:
        print("No table found in the document.")
        return

    rows = table.find_all('tr')
    
    headers = [td.get_text(strip=True) for td in rows[0].find_all(['th', 'td'])]
    
    try:
        x_idx = headers.index('x-coordinate')
        char_idx = headers.index('Character')
        y_idx = headers.index('y-coordinate')
    except ValueError:
        x_idx, char_idx, y_idx = 0, 1, 2

    data = []
    max_x = 0
    max_y = 0

    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 3:
            x = int(cols[x_idx].get_text(strip=True))
            char = cols[char_idx].get_text(strip=True)
            y = int(cols[y_idx].get_text(strip=True))
            
            data.append((x, y, char))
            if x > max_x: max_x = x
            if y > max_y: max_y = y

    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y, char in data:
        grid[y][x] = char

    for y in range(max_y, -1, -1):
        print("".join(grid[y]))

if __name__ == "__main__":
    print_secret_message("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")