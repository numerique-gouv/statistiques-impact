import { MigrationInterface, QueryRunner } from "typeorm";

export class RenameFrequenceCalcul1696860912476 implements MigrationInterface {
    name = 'RenameFrequenceCalcul1696860912476'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" RENAME COLUMN "frequence_calcul" TO "frequence_monitoring"`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" RENAME COLUMN "frequence_monitoring" TO "frequence_calcul"`);
    }

}
