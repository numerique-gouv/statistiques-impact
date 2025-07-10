import { Column, Entity, ManyToOne, OneToMany, PrimaryGeneratedColumn } from 'typeorm';
import { Indicator } from '../indicator';

@Entity()
export class Product {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column({ unique: true })
    nom_service_public_numerique: string;

    @OneToMany(() => Indicator, (indicator) => indicator.product)
    indicators: Indicator[];
}
