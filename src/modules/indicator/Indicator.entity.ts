import { Column, Entity, ManyToOne, PrimaryGeneratedColumn, Unique } from 'typeorm';
import { Product } from '../product';

@Unique('One unique value for indicator by frequence and date', [
    'product',
    'indicateur',
    'frequence_calcul',
    'date',
])
@Entity()
export class Indicator {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @ManyToOne(() => Product, { onDelete: 'CASCADE' })
    product: Product;

    @Column({ default: true })
    isAutomatic: boolean;

    @Column()
    indicateur: string;

    @Column('float')
    valeur: number;

    @Column()
    unite_mesure: string;

    @Column()
    frequence_calcul: string;

    @Column()
    date: string;

    @Column({ nullable: true })
    date_debut?: string;

    @Column()
    est_periode: boolean;
}
