<template>
  <div class="posts-container">
    <h1>Posts in Community {{ communityId }}</h1>

    <!-- Show a loading message or spinner while posts are being fetched -->
    <p v-if="isLoading">Loading posts...</p>

    <ul v-if="!isLoading">
      <li v-for="post in posts" :key="post.id">
        <!-- Display the author username next to the post title -->
        <router-link :to="`/forum/${communityId}/post/${post.id}`">
          {{ post.author_username ? post.author_username + ': ' : '' }}{{ post.title }}
        </router-link>
      </li>
    </ul>

    <!-- Create Post Button aligned to the left -->
    <router-link :to="`/forum/${communityId}/post/create`" class="create-post-btn">
      Create a Post
    </router-link>
  </div>
</template>

<script>
  import { useForumStore } from '../store/forum';
  import axios from 'axios';

  export default {
    props: ['communityId'],
    data() {
      return {
        posts: [], // Array to hold posts
        isLoading: true, // To track loading state
      };
    },
    async created() {
      const forumStore = useForumStore();

      try {
        // Fetch posts asynchronously
        await forumStore.fetchPosts(this.communityId);
        this.posts = forumStore.posts; // Bind the posts to the component state
      } catch (error) {
        console.error('Error fetching posts:', error);
      } finally {
        this.isLoading = false; // Set loading to false when done
      }
    },
  };
</script>

<style scoped>
  .posts-container {
    margin-top: 100px; 
    margin-left: 70px; 
    padding-right: 20px; 
    text-align: left; 
  }

  h1 {
    margin-bottom: 10px;
  }

  .posts-container ul {
    list-style-type: none;
    padding-left: 10px;
    margin-left: 10px;
    margin-top: 30px;
    text-align: left; 
  }

  .create-post-btn {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #b43de6;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    margin-left: 10px;
  }

  .create-post-btn:hover {
    background-color: #9b2bd3;
  }
</style>
