<template>
    <div class="post-detail-container">
      <h1>{{ post.title }}</h1>
      <p>{{ post.description }}</p>
  
      <!-- Replies Section -->
      <div class="reply-section">
        <h3>Replies</h3>
        <div class="replies">
          <div v-for="reply in post.replies" :key="reply.id" class="reply-item">
            <p><strong>{{ reply.author.username }}:</strong> {{ reply.content }}</p>
          </div>
        </div>
  
        <!-- Reply Form -->
        <form @submit.prevent="submitReply">
          <textarea v-model="newReply" placeholder="Write a reply..." required></textarea>
          <button type="submit">Submit Reply</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: ['communityId', 'postId'],
    data() {
      return {
        post: {},         // To store the post details
        newReply: '',     // To bind the new reply
      };
    },
    async created() {
      // Fetch the post details when the component is created
      await this.fetchPost();
    },
    methods: {
      // Fetch the post with its replies
      async fetchPost() {
        try {
          console.log("Fetching post with ID:", this.postId);  // Log the postId
          const response = await axios.get(`/api/posts/${this.postId}`);
          this.post = response.data; // Assuming the response contains post data
  
          // Ensure replies is always an array
          if (!this.post.replies) {
            this.post.replies = [];
          }
        } catch (error) {
          console.error('Error fetching post:', error);
        }
      },
  
      // Submit the new reply
      async submitReply() {
        try {
          const response = await axios.post(`/api/posts/${this.postId}/comments`, {
            content: this.newReply,
          });
  
          // Ensure replies is defined and then push the new reply
          if (!this.post.replies) {
            this.post.replies = [];
          }
  
          this.post.replies.push(response.data); // Add the new reply to the list of replies
          this.newReply = ''; // Clear the reply field
        } catch (error) {
          console.error('Error submitting reply:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .post-detail-container {
    margin-top: 100px;
    padding: 20px;
    text-align: left;
    margin-left: 50px;
  }
  
  .reply-section {
    margin-top: 20px;
  }
  
  .replies {
    display: flex;
    flex-direction: column;
    margin-top: 10px;
  }
  
  .reply-item {
    margin-bottom: 10px;
    padding-left: 0px;
    text-align: left;
    color: #eaeaea;
    background-color: #0d1019;
    border-radius: 5px;
    padding: 10px;
    margin-right: 20px;
  }
  
  .reply-section form {
    margin-top: 10px;
  }
  
  textarea {
    width: 100%;
    height: 100px;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>
  