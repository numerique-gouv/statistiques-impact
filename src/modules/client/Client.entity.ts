import { Column, Entity, ManyToOne, PrimaryGeneratedColumn } from 'typeorm';
import { Product } from '../product';

@Entity()
export class Client {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @ManyToOne(() => Product, { onDelete: 'CASCADE' })
    product: Product;

    @Column()
    secret: string;
}
