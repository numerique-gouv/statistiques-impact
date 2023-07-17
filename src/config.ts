import dotenv from 'dotenv';

dotenv.config();

const config = {
    PORT: process.env.PORT || 3000,
};

export { config };
