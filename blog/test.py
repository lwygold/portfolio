from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

        logo_btn = navbar.find('a', text="Do it DJANGO")
        self.assertEqual(logo_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text="About me")
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_post_list(self):
        self.assertEqual(2, 2)

        # 1.1 포스트 목록 페이지(post list)를 연다.
        response = self.client.get('/blog/')
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지의 타이틀에 Blog라는 문구가 있다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.assertIn('Blog', soup.title.text)
        # 2.1 게시물이 하나도 없을 때
        self.assertEqual(Post.objects.count(), 0)
        # 2.1 메인 영역에 "아직 게시물이 없습니다" 라는 문구가 나온다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        # 3.1 만약 게시물이 2개 있다면,
        post_001 = Post.objects.create(
            title = '첫번째 포스트입니다.',
            content = 'Helllo, World. We are the World.',
        )
        post_002 = Post.objects.create(
            title='두번째 포스트입니다.',
            content='마라탕 ',
        )
        self.assertEqual(Post.objects.count(), 2)
        # 3.2 포스트 목록 페이지를 새로 고침했을 때,
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 "아직 게시물이 없습니다" 라는 문구가 없어야 한다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        # 1.1 포스트가 하나 있다.
        post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Helllo, World. We are the World.',
        )
        self.assertEqual(Post.objects.count(),1)
        # 1.2 그 포스트의 url은 '/blog/1/' 이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 2.1 첫 번째 포스트의 상세 페이지가 온다.
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        # 2.2 첫 번째 포스트
        soup = BeautifulSoup(response.content, 'html.parser')
        # 2.2
        self.navbar_test(soup)

        # 2.3
        self.assertIn(post_001.title, soup.title.text)
        # 2.4
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        # 2.5
        # 2.6
        self.assertIn(post_001.content, post_area.text)






