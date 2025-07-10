import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class LogEntry {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column()
    description: string;
}
