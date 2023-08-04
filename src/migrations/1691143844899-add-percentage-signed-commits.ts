import { MigrationInterface, QueryRunner } from "typeorm";

export class AddPercentageSignedCommits1691143844899 implements MigrationInterface {
    name = 'AddPercentageSignedCommits1691143844899'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "product" ADD "percentageSignedCommits" double precision`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "product" DROP COLUMN "percentageSignedCommits"`);
    }

}
