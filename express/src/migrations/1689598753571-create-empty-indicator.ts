import { MigrationInterface, QueryRunner } from 'typeorm';

export class CreateEmptyIndicator1689598753571 implements MigrationInterface {
    name = 'CreateEmptyIndicator1689598753571';

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(
            `CREATE TABLE "indicator" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "nom_service_public_numerique" character varying NOT NULL, CONSTRAINT "PK_4693fe4c2cb912a71e05c589e7e" PRIMARY KEY ("id"))`,
        );
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DROP TABLE "indicator"`);
    }
}
