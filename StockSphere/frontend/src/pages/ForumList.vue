<template>
    <div class="forum-container">
      <h1 class="forum-title">Forum Communities</h1>
  
      <!-- Button to open the modal -->
      <button @click="showModal = true" class="create-btn">Create a Community</button>
  
      <!-- Modal for creating a community -->
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <h2>Create a Community</h2>
          <form @submit.prevent="createCommunity">
            <div class="form-group">
              <label for="name">Community Name</label>
              <input v-model="community.name" id="name" type="text" required placeholder="Enter community name" />
            </div>
  
            <div class="form-group">
              <label for="description">Community Description</label>
              <textarea v-model="community.description" id="description" required placeholder="Enter community description"></textarea>
            </div>
  
            <div class="form-actions">
              <button type="submit" class="submit-btn">Create Community</button>
              <button type="button" @click="closeModal" class="cancel-btn">Cancel</button>
            </div>
          </form>
        </div>
      </div>
  
      <ul>
        <li v-for="community in communities" :key="community.id">
          <router-link :to="`/forum/${community.id}`">{{ community.name }}</router-link>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { useForumStore } from '../store/forum';
  import axios from '../axios';
  
  export default {
    data() {
      return {
        communities: [],
        showModal: false, // Controls the visibility of the modal
        community: {
          name: '',
          description: '',
        },
      };
    },
    created() {
      const forumStore = useForumStore();
      forumStore.fetchCommunities();
      this.communities = forumStore.communities;
    },
    methods: {
      async createCommunity() {
        try {
          // Send POST request to create the community
          await axios.post('/api/communities/', this.community);
          
          // Fetch updated list of communities after creation
          this.fetchCommunities();
  
          // Close the modal and reset the form
          this.closeModal();
          this.community = { name: '', description: '' };
  
          alert('Community created successfully!');
        } catch (error) {
          console.error('Error creating community:', error);
          alert('There was an error creating the community.');
        }
      },
      async fetchCommunities() {
        try {
          const response = await axios.get('/api/communities/');
          this.communities = response.data;
        } catch (error) {
          console.error('Error fetching communities:', error);
        }
      },
      closeModal() {
        this.showModal = false;
      },
    },
  };
  </script>
  
  <style scoped>
  /* Modal Overlay */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7); /* Darken the background */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    margin-top: 60px; /* Push down if app bar height is 60px */
  }
  
  /* Modal Content */
  .modal-content {
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    width: 400px; /* Adjusted width */
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  /* Form styling */
  .form-group {
    margin-bottom: 15px;
    text-align: left;
  }
  
  .form-group input,
  .form-group textarea {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
  }
  
  /* Buttons */
  .submit-btn,
  .cancel-btn {
    width: 48%;
    padding: 10px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
  }
  
  .submit-btn {
    background-color: #4CAF50;
    color: white;
  }
  
  .cancel-btn {
    background-color: #f44336;
    color: white;
    margin-left: 4%;
  }
  
  .submit-btn:hover {
    background-color: #45a049;
  }
  
  .cancel-btn:hover {
    background-color: #e53935;
  }
  
  /* Modal Actions */
  .form-actions {
    display: flex;
    justify-content: space-between;
  }
  
  /* Forum Page */
  .forum-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    padding: 20px;
    height: 100vh; /* Full height */
    margin-top: 100px; /* Push the entire page down to clear the app bar */
    margin-left: 50px;
  }
  
  .create-btn {
    padding: 10px 20px;
    background-color: #b43de6;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin-bottom: 20px;
  }
  
  .create-btn:hover {
    background-color: #9b2bd3;
  }
  
  /* Add additional styling for responsive layouts */
  @media (max-width: 600px) {
    .modal-content {
      width: 90%;
    }
  
    .create-btn {
      width: 100%;
    }
  }
  </style>
  