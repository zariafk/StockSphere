<template>
  <div class="create-community-container">
    <h2>Create a Community</h2>
    <!-- To create a community -->
    <form @submit.prevent="createCommunity" class="community-form">
      <div class="form-group">
        <label for="name">Community Name</label>
        <input v-model="community.name" id="name" type="text" required />
      </div>
      <div class="form-group">
        <label for="description">Community Description</label>
        <textarea v-model="community.description" id="description" required></textarea>
      </div>

      <button type="submit" class="submit-btn">Create Community</button>
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
