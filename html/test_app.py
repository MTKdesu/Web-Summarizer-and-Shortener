import pytest
from app import app as flask_app
from app import init_db,insert_url_mapping,query_original_url,cleanup_test_data

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        # Configure a test database if necessary
    })
    # Initialize the database
    init_db()

    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Web Link Shorten' in response.get_data(as_text=True)

def test_url_shortening(client):
    """Test URL shortening functionality."""
    original_url = 'http://example.com'
    response = client.post('/', data={'url': original_url})
    assert response.status_code == 200
    # 假设返回的短链接在 JSON 响应体中的 'short_url' 键下
    json_data = response.get_json()
    assert 'short_url' in json_data
    # 验证短链接的格式

def test_redirect_to_url(client):
    """测试短链接重定向到原始URL"""
    # 插入测试数据到数据库
    original_url = 'http://example.com'
    short_path = 'abc123'  # 假定这是根据某种逻辑生成的短链接路径
    insert_url_mapping(original_url, short_path)

    # 执行重定向测试
    response = client.get(f'/{short_path}', follow_redirects=False)
    assert response.status_code == 302, "重定向时应返回302状态码"
    assert 'Location' in response.headers, "响应头应包含Location"
    expected_url = original_url
    assert response.headers['Location'] == expected_url, f"应重定向到 {expected_url}"

    cleanup_test_data(original_url, short_path)

def test_database_operations(client):
    """测试数据库操作，包括插入和查询URL映射"""
    original_url = 'http://example.com/test'
    short_path = 'xyz789'  # 假定这是根据某种逻辑生成的短链接路径
    insert_url_mapping(original_url, short_path)  # 假设这是应用中用于插入数据的函数
    retrieved_url = query_original_url(short_path)  # 假设这是应用中用于查询数据的函数
    assert retrieved_url == original_url, "查询到的原始URL应与插入的URL相匹配"

    # 清理测试数据
    cleanup_test_data(original_url, short_path)

def test_submit_invalid_url(client):
    """测试提交无效URL时的行为"""
    invalid_url = 'not_a_valid_url'
    response = client.post('/', data={'url': invalid_url})
    # 假设您希望应用返回400 Bad Request状态码以表示输入无效
    assert response.status_code == 400, "提交无效URL应返回400状态码"