<template>
    <div class="post-detail-container">
      <!-- Display Author's Username above the Post Title -->
      <div class="post-header">
        <h3 class="author-username">
          <span v-if="post.author_username">{{ post.author_username }}</span>
          <span v-if="!post.author_username">Anonymous</span>
        </h3>
        <h1 class="post-title">{{ post.title }}</h1>
      </div>
  
      <!-- Post Description Below the Title -->
      <p class="post-description">{{ post.content }}</p>
  
      <!-- Comments Section -->
      <div class="comment-section">
        <h3>Comments</h3>
        <div class="comments">
          <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
            <!-- Display the author username or 'Anonymous' if no username exists -->
            <p><strong>{{ comment.author_username ? comment.author_username : 'Anonymous' }}:</strong> {{ comment.content }}</p>
          </div>
        </div>
  
        <!-- Comment Form -->
        <form @submit.prevent="submitComment">
          <textarea v-model="newComment" placeholder="Write a comment..." required></textarea>
          <button type="submit">Submit Comment</button>
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
        newComment: '',   // To bind the new comment
      };
    },
    async created() {
      // Fetch the post details when the component is created
      await this.fetchPost();
    },
    methods: {
      async fetchPost() {
        try {
          // Fetch the post with its comments
          const response = await axios.get(`/api/posts/${this.postId}`);
          console.log("Fetched Post Data:", response.data);
  
          this.post = response.data;
  
          // Log the comments and their author usernames to verify correct data
          this.post.comments.forEach(comment => {
            console.log(`Comment Author: ${comment.author_username}`);
          });
  
        } catch (error) {
          console.error('Error fetching post:', error);
        }
      },
  
      // Submit the new comment
      async submitComment() {
        try {
          const response = await axios.post(`/api/posts/${this.postId}/comments`, {
            content: this.newComment,
          });
  
          // Ensure comments are defined and then push the new comment
          if (!this.post.comments) {
            this.post.comments = [];
          }
  
          this.post.comments.push(response.data); // Add the new comment to the list of comments
          this.newComment = ''; // Clear the comment field
        } catch (error) {
          console.error('Error submitting comment:', error);
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
  
  .post-header {
    margin-bottom: 5px; 
  }
  
  .author-username {
    font-size: 1.2em;
    color: #666;
    font-weight: bold;
    margin: 0; 
  }
  
  .post-title {
    font-size: 2.5em;
    color: #eaeaea;  
    margin: 0; 
  }
  
  .post-description {
    font-size: 1.2em;
    color: #eaeaea;  
    margin-top: 10px; 
  }
  
  .comment-section {
    margin-top: 30px;
  }
  
  .comments {
    display: flex;
    flex-direction: column;
    margin-top: 10px;
  }
  
  .comment-item {
    margin-bottom: 10px;
    padding-left: 0px;
    text-align: left;
    color: #eaeaea;
    background-color: #0d1019;
    border-radius: 5px;
    padding: 10px;
    margin-right: 20px;
  }
  
  .comment-section form {
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
    background-color: #b43de6;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #9b2bd3;
  }
</style>
  