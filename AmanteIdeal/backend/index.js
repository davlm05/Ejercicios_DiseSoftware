import express from 'express';
import cors from 'cors';
import { connectDB } from './config/db.js';
import amanteRoutes from './routes/amante.routes.js';
import { Amante } from './models/amante.model.js';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/amantes', amanteRoutes);

// Connect to DB and start server
connectDB().then(async () => {
    // Seed Minimal Data mapping specifically on boot up
    const count = await Amante.countDocuments();
    if (count === 0) {
        console.log('Seeding initial data...');
        await Amante.create([
            { nombre: 'Juan Perez', edad: 25, intereses: ['viajar', 'comer', 'leer'] },
            { nombre: 'Maria Gomez', edad: 29, intereses: ['cine', 'musica'] }
        ]);
        console.log('Seed data inserted');
    }

    app.listen(PORT, () => {
        console.log(`Server is running on http://127.0.0.1:${PORT}`);
    });
});
