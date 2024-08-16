import axios from 'axios';

export const signupUser = async (data: { family_name: string; first_name: string; username: string; password: string; }) => {
    try {
        const response = await axios.post('/api/signup/', data);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw new Error(error.response.data.detail || 'Error during signup');
        } else {
            throw new Error('Unexpected error occurred');
        }
    }
};
