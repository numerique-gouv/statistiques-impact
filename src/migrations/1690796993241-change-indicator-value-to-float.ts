import { MigrationInterface, QueryRunner } from 'typeorm';

export class ChangeIndicatorValueToFloat1690796993241 implements MigrationInterface {
    name = 'ChangeIndicatorValueToFloat1690796993241';

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DELETE FROM "indicator"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "valeur"`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "valeur" double precision NOT NULL`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DELETE FROM "indicator"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "valeur"`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "valeur" integer NOT NULL`);
    }
}
