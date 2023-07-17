import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Indicator {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column()
    nom_service_public_numerique: string;

    @Column()
    indicateur: string;

    @Column()
    valeur: number;

    @Column()
    unite_mesure: string;

    @Column()
    frequence_calcul: string;

    @Column({ type: 'timestamptz' })
    date: string;

    @Column()
    est_periode: boolean;
}
