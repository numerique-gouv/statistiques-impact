import { MigrationInterface, QueryRunner } from "typeorm";

export class AddDateDebut1689690449419 implements MigrationInterface {
    name = 'AddDateDebut1689690449419'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" ADD "date_debut" character varying`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "date_debut"`);
    }

}
