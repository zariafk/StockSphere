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

    <!-- Show a loading message if data is being fetched -->
    <p v-if="isLoading">Loading communities...</p>

    <ul v-if="!isLoading">
      <li v-for="community in communities" :key="community.id">
        <router-link :to="`/forum/${community.id}`">{{ community.name }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
  import { useForumStore } from '../store/forum';  // Assuming you're using a Vuex store
  import axios from '../axios';  // Axios instance to interact with the API

  export default {
    data() {
      return {
        isLoading: false,
        communities: [],  // List of communities to display
        showModal: false,  // Controls visibility of the modal for creating a new community
        community: {
          name: '',
          description: '',
        },
      };
    },
    async created() {
      const forumStore = useForumStore();  // Access the Vuex store
      await forumStore.fetchCommunities();  // Fetch communities from the store
      this.communities = forumStore.communities;  // Set the component's communities list
    },
    methods: {
      // Method to create a new community
      async createCommunity() {
        try {
          // Send POST request to create the new community
          await axios.post('/api/communities/', this.community);
          
          // Fetch updated list of communities after creation
          await this.fetchCommunities();

          // Close the modal and reset the form
          this.closeModal();
          this.community = { name: '', description: '' };

          alert('Community created successfully!');
        } catch (error) {
          console.error('Error creating community:', error);
          alert('There was an error creating the community.');
        }
      },

      // Method to fetch communities from the API and update the local state
      async fetchCommunities() {
        try {
          const response = await axios.get('/api/communities/');
          console.log(response.data);  // Log the response to check the fetched communities
          this.communities = response.data;  // Update the component's community list
        } catch (error) {
          console.error('Error fetching communities:', error);
        }
      },

      // Method to close the modal
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
}

/* Modal Content */
.modal-content {
  background: #1b1e27;
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
  border: 1px solid #eaeaea;
  border-radius: 5px;
  font-size: 14px;
}

/* Buttons */
.submit-btn,
.cancel-btn {
  width: 48%;
  padding: 10px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.submit-btn {
  background-color: #b43de6;
  border: none;
  color: white;
}

.cancel-btn {
  background-color: #1b1e27;
  color: white;
  margin-left: 4%;
  border-width: 3px;
  border-color: #b43de6;
}

.submit-btn:hover {
  background-color: #9b2bd3;
}

.cancel-btn:hover {
  background-color: #171a23;
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

ul {
  list-style-type: none; /* Remove bullet points */
  padding: 0; /* Remove padding */
  color: #eaeaea;
}

li {
  margin-bottom: 10px; /* Add space between list items */
  font-size: 18px; /* Optional: Adjust text size */
  padding-left: 5px; /* Optional: Add left padding */
  color: #eaeaea;
}

a {
  color: #eaeaea; /* Ensure links are also dark gray */
  text-decoration: none; /* Remove underline */
}

a:hover {
  color: #d4d4d4; /* Optional: Change color of the link when hovered */
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
