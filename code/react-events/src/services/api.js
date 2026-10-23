import axios from 'axios';

const API_URL = 'http://localhost:8181/events';

export const getEvents = async () => {
  try {
    const response = await axios.get(API_URL);
    return response.data;
  } catch (error) {
    console.error('Failed to retrieve event:', error);
    throw error;
  }
};

export const createEvent = async (event) => {
  try {
    const response = await axios.post(API_URL, event);
    return response.data;
  } catch (error) {
    console.error('Event creation failed:', error);
    throw error;
  }
};

export const updateEvent = async (id, event) => {
  try {
    const response = await axios.put(`${API_URL}/${id}`, event);
    return response.data;
  } catch (error) {
    console.error('Update event failed:', error);
    throw error;
  }
};

export const deleteEvent = async (id) => {
  try {
    await axios.delete(`${API_URL}/${id}`);
  } catch (error) {
    console.error('Failed to delete event:', error);
    throw error;
  }
};