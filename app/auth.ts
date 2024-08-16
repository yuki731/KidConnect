import axios from 'axios';

export const signupUser = async (userData: {
    username: string;
    password: string;
    birthdate: string;
    address?: string;
    family_name: string;
    first_name: string;
}) => {
    try {
        const response = await axios.post('/api/signup/', userData);
        return response.data;
    } catch (error) {
        throw error.response?.data || "Error during signup";
    }
};
