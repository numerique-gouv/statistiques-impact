import { Column, Entity, ManyToOne, PrimaryGeneratedColumn, Unique } from 'typeorm';
import { Product } from '../product';

@Unique('One client access for one product', ['product'])
@Entity()
export class Client {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @ManyToOne(() => Product)
    product: Product;

    @Column()
    secret: string;
}
