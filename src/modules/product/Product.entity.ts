import { Column, Entity, OneToMany, PrimaryGeneratedColumn } from 'typeorm';
import { Indicator } from '../indicator';

@Entity()
export class Product {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column({ unique: true })
    nom_service_public_numerique: string;

    @Column({ nullable: true })
    metabaseVersion?: string;

    @Column('float', { nullable: true })
    percentageSignedCommits?: number;

    @OneToMany(() => Indicator, (indicator) => indicator.product)
    indicators: Indicator[];
}
