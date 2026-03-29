import mongoose from 'mongoose';

const amanteSchema = new mongoose.Schema({
    nombre: { type: String, required: true },
    edad: { type: Number, required: true },
    intereses: [{ type: String, required: true }]
}, { timestamps: true });

export const Amante = mongoose.model('Amante', amanteSchema);
