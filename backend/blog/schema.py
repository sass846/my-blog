import graphene
from django.db.models import Count
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from blog import models

class UserType(DjangoObjectType):
	class Meta:
		model = get_user_model()

class AuthorType(DjangoObjectType):
	class Meta:
		model = models.Profile

class PostType(DjangoObjectType):
	class Meta:
		model = models.Post

class TagType(DjangoObjectType):
	post_count = graphene.Int()

	class Meta:
		model = models.Tag

class Query(graphene.ObjectType):
	all_posts = graphene.List(PostType)
	tags_by_post_count = graphene.List(TagType)
	author_by_username = graphene.Field(AuthorType, username=graphene.String())
	post_by_slug = graphene.Field(PostType, slug=graphene.String())
	posts_by_author = graphene.List(PostType, username=graphene.String())
	posts_by_tag = graphene.List(PostType, tag=graphene.String())

	def resolve_all_posts(self, info):
		return (
			models.Post.objects.prefetch_related("tags")
			.select_related("author")
			.all()
		)
	
	def resolve_author_by_username(self, info, username):
		return (
			models.Post.objects.select_related("author").get(
				user__username = username
			)
		)

	def resolve_post_by_slug(self, info, slug):
		return (
			models.Post.objects.prefetch_related("tags")
			.select_related("author")
			.get(slug=slug)
		)

	def resolve_posts_by_author(self, info, username):
		return (
			models.Post.objects.prefetch_related("tags")
			.select_related("author")
			.filter(author__user__username=username)
		)

	def resolve_posts_by_tag(self, info, tag):
		return (
			models.Post.objects.prefetch_related("tags")
			.select_related("author")
			.filter(tags__name__iexact=tag)
		)

	def resolve_tags_by_post_count(self, info):
		return (
			models.Tag.objects.annotate(post_count=Count("post"))
			.order_by("-post_count")
		)

schema = graphene.Schema(query=Query)