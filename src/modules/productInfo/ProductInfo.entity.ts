import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class ProductInfo {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column({ unique: true })
    nom_service_public_numerique: string;

    @Column({ nullable: true })
    metabaseVersion: string;
}
