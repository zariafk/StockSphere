<template>
  <div class="create-post-container">
    <h1>Create a Post in Community {{ communityId }}</h1>
    
    <!-- Create a post -->
    <form @submit.prevent="createPost" class="post-form">
      <div class="form-group">
        <label for="title">Post Title</label>
        <input 
          v-model="title" 
          type="text" 
          id="title" 
          placeholder="Post Title" 
          required 
          class="form-input"
        />
      </div>
      
      <div class="form-group">
        <label for="content">Post Content</label>
        <textarea 
          v-model="content" 
          id="content" 
          placeholder="Write your post content here..." 
          required 
          class="form-input"
        ></textarea>
      </div>

      <!-- Submit Button (Full Width) -->
      <button type="submit" class="submit-button">Submit</button>

      <!-- Cancel Button (Full Width) -->
      <button type="button" @click="cancelPost" class="cancel-button">Cancel</button>
    </form>
  </div>
</template>

<script>
import axios from '../axios'; // Make sure you have the correct import for axios

export default {
  props: ['communityId'],
  data() {
    return {
      title: '',
      content: '',
    };
  },
  methods: {
    async createPost() {
      try {
        // Log the communityId to ensure it's correct
        console.log('Community ID:', this.communityId);
        const communityIdInt = parseInt(this.communityId, 10);

        await axios.post('/api/posts/', {
          title: this.title,
          content: this.content,
          community: communityIdInt,
        });

        this.$router.push(`/forum/${communityIdInt}`);
        alert('Post created successfully!');
      } catch (error) {
        console.error('Error creating post:', error);
        alert('There was an error creating the post.');
      }
    },

    // Method to cancel the creation of the post
    cancelPost() {
      this.title = '';
      this.content = '';
      this.$router.push(`/forum/${this.communityId}`); // Navigate back to the community page
    }
  },
};
</script>

<style scoped>
  .create-post-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    margin-top: 100px;
    margin-left: 50px;
    background-color: #1b1e27;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }

  h1 {
    text-align: center;
    color: #eaeaea;
    margin-bottom: 20px;
  }

  .post-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
  }

  label {
    font-size: 16px;
    color: #eaeaea;
    margin-bottom: 8px;
  }

  .form-input {
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
    color: #eaeaea;
    margin-bottom: 10px;
    width: 100%;
  }

  .form-input:focus {
    border-color: #9b2bd3;
    outline: none;
  }

  .submit-button {
    padding: 12px;
    background-color: #b43de6;
    color: #eaeaea;
    font-size: 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
  }

  .submit-button:hover {
    background-color: #9b2bd3;
  }

  .submit-button:focus {
    outline: none;
  }

  .cancel-button {
    padding: 12px;
    background-color: #1b1e27;
    color: #eaeaea;
    font-size: 16px;
    border-radius: 4px;
    border-color: #b43de6;
    border-width: 2px;
    cursor: pointer;
    width: 100%;
    margin-top: 10px;
  }

  .cancel-button:hover {
    background-color: #171a23;
  }

  .cancel-button:focus {
    outline: none;
  }
</style>
