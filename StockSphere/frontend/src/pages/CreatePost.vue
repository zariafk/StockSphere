<template>
    <div>
      <h1>Create a Post in Community {{ communityId }}</h1>
      <form @submit.prevent="createPost">
        <input v-model="title" placeholder="Post Title" required />
        <textarea v-model="content" placeholder="Post Content" required></textarea>
        <button type="submit">Submit</button>
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
          // Ensure the communityId is an integer (though this should already be the case if it's passed correctly)
          const communityIdInt = parseInt(this.communityId, 10);
  
          // Log the data to make sure it's being sent correctly
          console.log('Creating post:', {
            title: this.title,
            content: this.content,
            community: communityIdInt, // Ensure communityId is being sent as an integer
          });
  
          // Send the POST request to create the post in the community
          await axios.post('/api/posts/', {
            title: this.title,
            content: this.content,
            community: communityIdInt, // Pass the correct communityId (integer)
          });
  
          // After successful creation, redirect to the community page
          this.$router.push(`/forum/${communityIdInt}`); // Use communityIdInt here, not this.communityId
          alert('Post created successfully!');
        } catch (error) {
          console.error('Error creating post:', error);
          alert('There was an error creating the post.');
        }
      },
    },
  };
  </script>
  