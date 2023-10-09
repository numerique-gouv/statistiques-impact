import { MigrationInterface, QueryRunner } from "typeorm";

export class RenameAutomatise1696860729585 implements MigrationInterface {
    name = 'RenameAutomatise1696860729585'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" RENAME COLUMN "isAutomatic" TO "est_automatise"`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" RENAME COLUMN "est_automatise" TO "isAutomatic"`);
    }

}
