import { Column, Entity, ManyToOne, PrimaryGeneratedColumn, Unique } from 'typeorm';

@Unique('One unique value for indicator by frequence and date', [
    'nom_service_public_numerique',
    'indicateur',
    'frequence_calcul',
    'date',
])
@Entity()
export class Indicator {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column()
    nom_service_public_numerique: string;

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
