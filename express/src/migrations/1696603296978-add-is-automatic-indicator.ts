import { MigrationInterface, QueryRunner } from "typeorm";

export class AddIsAutomaticIndicator1696603296978 implements MigrationInterface {
    name = 'AddIsAutomaticIndicator1696603296978'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" ADD "isAutomatic" boolean NOT NULL DEFAULT true`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "isAutomatic"`);
    }

}
