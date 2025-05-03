<template>
    <div class="posts-container">
      <h1>Posts in Community {{ communityId }}</h1>
      <ul>
        <li v-for="post in posts" :key="post.id">{{ post.title }}</li>
      </ul>
      <router-link :to="`/forum/${communityId}/post/create`">Create a Post</router-link>
    </div>
  </template>
  
  <script>
  import { useForumStore } from '../store/forum';
  import axios from 'axios';
  
  export default {
    props: ['communityId'],
    data() {
      return {
        posts: [],
      };
    },
    created() {
      const forumStore = useForumStore();
      forumStore.fetchPosts(this.communityId);
      this.posts = forumStore.posts;
    },
  };
  </script>
  
  <style scoped>
  .posts-container {
    margin-top: 80px; /* Adjust this value according to your app bar height */
    margin-left: 20px; /* Move content to the right */
    padding-right: 20px; /* Optional: padding for better spacing */
  }
  
  h1 {
    margin-bottom: 10px;
  }
  </style>
  