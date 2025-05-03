<template>
    <div class="posts-container">
      <h1>Posts in Community {{ communityId }}</h1>
  
      <!-- Show a loading message or spinner while posts are being fetched -->
      <p v-if="isLoading">Loading posts...</p>
  
      <ul v-if="!isLoading">
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
          margin-top: 100px; /* Adjust this value according to your app bar height */
          margin-left: 70px; /* Move content to the right */
          padding-right: 20px; /* Optional: padding for better spacing */
        }
        
        h1 {
          margin-bottom: 10px;
        }
        
        .posts-container ul {
          list-style-type: none;
          padding-left: 0px;
          margin-left: 10px;
        }
        
        .router-link {
          display: inline-block;
          margin-top: 20px; /* Optional: some spacing above the button */
        }
        </style>
        