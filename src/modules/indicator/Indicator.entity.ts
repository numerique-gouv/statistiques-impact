import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Indicator {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column()
    nom_service_public_numerique: string;
}
