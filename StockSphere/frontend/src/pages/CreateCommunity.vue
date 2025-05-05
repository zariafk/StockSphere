<template>
    <div>
      <h2>Create a Community</h2>
      <form @submit.prevent="createCommunity">
        <div>
          <label for="name">Community Name</label>
          <input v-model="community.name" id="name" type="text" required />
        </div>
  
        <div>
          <label for="description">Community Description</label>
          <textarea v-model="community.description" id="description" required></textarea>
        </div>
  
        <button type="submit">Create Community</button>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import axios from 'axios';
  
  export default {
    data() {
      return {
        community: {
          name: '',
          description: '',
        },
      };
    },
    methods: {
      async createCommunity() {
        try {
          // Send POST request to the backend to create a community
          const response = await axios.post('/api/communities/', this.community);
  
          // Optionally redirect or show success message
          this.$router.push('/forum'); // Redirect to the forum after community is created
          alert('Community created successfully!');
        } catch (error) {
          console.error('Error creating community:', error);
          alert('There was an error creating the community.');
        }
      },
    },
  };
  </script>
  